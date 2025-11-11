"""
Moderation commands cog.
Contains commands for server moderation like kick, ban, etc.
"""

import discord
from discord.ext import commands
from typing import Optional


class Moderation(commands.Cog):
    """Moderation commands for server management."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Kick a member from the server.
        
        Usage: !kick @member [reason]
        Example: !kick @John Spamming in chat
        
        Requires: Kick Members permission
        """
        if member == ctx.author:
            await ctx.send("❌ You cannot kick yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot kick someone with a higher or equal role!")
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ I cannot kick someone with a higher or equal role than me!")
            return
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title="✅ Member Kicked",
                color=discord.Color.orange(),
                description=f"{member.mention} has been kicked from the server."
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to kick this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Ban a member from the server.
        
        Usage: !ban @member [reason]
        Example: !ban @John Repeated rule violations
        
        Requires: Ban Members permission
        """
        if member == ctx.author:
            await ctx.send("❌ You cannot ban yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot ban someone with a higher or equal role!")
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send("❌ I cannot ban someone with a higher or equal role than me!")
            return
        
        try:
            await member.ban(reason=reason, delete_message_days=1)
            
            embed = discord.Embed(
                title="🔨 Member Banned",
                color=discord.Color.red(),
                description=f"{member.mention} has been banned from the server."
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to ban this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, user_id: int, *, reason: Optional[str] = "No reason provided"):
        """
        Unban a user from the server.
        
        Usage: !unban <user_id> [reason]
        Example: !unban 123456789012345678 Appeal accepted
        
        Requires: Ban Members permission
        """
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title="✅ User Unbanned",
                color=discord.Color.green(),
                description=f"{user.mention} ({user.name}) has been unbanned."
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {user_id}")
            
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send("❌ User not found or not banned.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to unban users.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")
    
    @commands.command(name='clear', aliases=['purge', 'delete'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int = 10):
        """
        Delete multiple messages from the channel.
        
        Usage: !clear [amount]
        Example: !clear 50
        
        Default: 10 messages
        Maximum: 100 messages
        Requires: Manage Messages permission
        """
        if amount < 1:
            await ctx.send("❌ Amount must be at least 1.")
            return
        
        if amount > 100:
            await ctx.send("❌ Amount cannot exceed 100 messages.")
            return
        
        try:
            # Delete the command message and the specified amount of messages
            deleted = await ctx.channel.purge(limit=amount + 1)
            
            # Send confirmation message that will auto-delete
            msg = await ctx.send(f"✅ Deleted {len(deleted) - 1} message(s).")
            await msg.delete(delay=5)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to delete messages.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")
    
    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member, duration: Optional[int] = 60, *, reason: Optional[str] = "No reason provided"):
        """
        Timeout a member (mute them temporarily).
        
        Usage: !mute @member [duration_in_minutes] [reason]
        Example: !mute @John 30 Spamming
        
        Default duration: 60 minutes
        Requires: Moderate Members permission
        """
        if member == ctx.author:
            await ctx.send("❌ You cannot mute yourself!")
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send("❌ You cannot mute someone with a higher or equal role!")
            return
        
        if duration < 1 or duration > 40320:  # Max 28 days (40320 minutes)
            await ctx.send("❌ Duration must be between 1 and 40320 minutes (28 days).")
            return
        
        try:
            import datetime
            timeout_until = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=reason)
            
            embed = discord.Embed(
                title="🔇 Member Muted",
                color=discord.Color.orange(),
                description=f"{member.mention} has been muted."
            )
            embed.add_field(name="Duration", value=f"{duration} minutes", inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to timeout this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")
    
    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def unmute(self, ctx, member: discord.Member, *, reason: Optional[str] = "No reason provided"):
        """
        Remove timeout from a member (unmute them).
        
        Usage: !unmute @member [reason]
        Example: !unmute @John Time served
        
        Requires: Moderate Members permission
        """
        try:
            await member.timeout(None, reason=reason)
            
            embed = discord.Embed(
                title="🔊 Member Unmuted",
                color=discord.Color.green(),
                description=f"{member.mention} has been unmuted."
            )
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=True)
            embed.set_footer(text=f"User ID: {member.id}")
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to remove timeout from this member.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Moderation(bot))
