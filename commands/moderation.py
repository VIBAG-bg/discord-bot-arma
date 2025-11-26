import discord
from discord.ext import commands
from typing import Optional
from dms.localization import t
from database.service import get_or_create_user_from_member


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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        if member == ctx.author:
            await ctx.send(t(lang, "mod_cannot_target_self_kick"))
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send(t(lang, "mod_cannot_target_higher"))
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send(t(lang, "mod_bot_cannot_target_higher"))
            return
        
        try:
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title=t(lang, "mod_kick_title"),
                color=discord.Color.orange(),
                description=t(lang, "mod_kick_description").format(member=member.mention)
            )
            embed.add_field(name=t(lang, "mod_reason"), value=reason, inline=False)
            embed.add_field(name=t(lang, "mod_moderator"), value=ctx.author.mention, inline=True)
            embed.set_footer(text=t(lang, "mod_user_id").format(user_id=member.id))
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_kick"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))
    
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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        if member == ctx.author:
            await ctx.send(t(lang, "mod_cannot_target_self_ban"))
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send(t(lang, "mod_cannot_target_higher"))
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send(t(lang, "mod_bot_cannot_target_higher"))
            return
        
        try:
            await member.ban(reason=reason, delete_message_days=1)
            
            embed = discord.Embed(
                title=t(lang, "mod_ban_title"),
                color=discord.Color.red(),
                description=t(lang, "mod_ban_description").format(member=member.mention)
            )
            embed.add_field(name=t(lang, "mod_reason"), value=reason, inline=False)
            embed.add_field(name=t(lang, "mod_moderator"), value=ctx.author.mention, inline=True)
            embed.set_footer(text=t(lang, "mod_user_id").format(user_id=member.id))
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_ban"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))
    
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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title=t(lang, "mod_unban_title"),
                color=discord.Color.green(),
                description=t(lang, "mod_unban_description").format(user=user.mention, name=user.name)
            )
            embed.add_field(name=t(lang, "mod_reason"), value=reason, inline=False)
            embed.add_field(name=t(lang, "mod_moderator"), value=ctx.author.mention, inline=True)
            embed.set_footer(text=t(lang, "mod_user_id").format(user_id=user_id))
            
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(t(lang, "mod_user_not_found_or_not_banned"))
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_unban"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))
    
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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        if amount < 1:
            await ctx.send(t(lang, "mod_clear_amount_min"))
            return
        
        if amount > 100:
            await ctx.send(t(lang, "mod_clear_amount_max"))
            return
        
        try:
            # Delete the command message and the specified amount of messages
            deleted = await ctx.channel.purge(limit=amount + 1)
            
            # Send confirmation message that will auto-delete
            msg = await ctx.send(t(lang, "mod_clear_deleted").format(count=len(deleted) - 1))
            await msg.delete(delay=5)
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_clear"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))
    
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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        if member == ctx.author:
            await ctx.send(t(lang, "mod_cannot_target_self_mute"))
            return
        
        if member.top_role >= ctx.author.top_role:
            await ctx.send(t(lang, "mod_cannot_target_higher"))
            return
        
        if duration < 1 or duration > 40320:  # Max 28 days (40320 minutes)
            await ctx.send(t(lang, "mod_mute_duration_invalid"))
            return
        
        try:
            import datetime
            timeout_until = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
            await member.timeout(timeout_until, reason=reason)
            
            embed = discord.Embed(
                title=t(lang, "mod_mute_title"),
                color=discord.Color.orange(),
                description=t(lang, "mod_mute_description").format(member=member.mention)
            )
            embed.add_field(
                name=t(lang, "mod_duration"),
                value=t(lang, "mod_duration_minutes").format(minutes=duration),
                inline=True,
            )
            embed.add_field(name=t(lang, "mod_reason"), value=reason, inline=False)
            embed.add_field(name=t(lang, "mod_moderator"), value=ctx.author.mention, inline=True)
            embed.set_footer(text=t(lang, "mod_user_id").format(user_id=member.id))
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_mute"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))
    
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
        lang = "en"
        if isinstance(ctx.author, discord.Member):
            user = get_or_create_user_from_member(ctx.author)
            lang = user.language or "en"
        try:
            await member.timeout(None, reason=reason)
            
            embed = discord.Embed(
                title=t(lang, "mod_unmute_title"),
                color=discord.Color.green(),
                description=t(lang, "mod_unmute_description").format(member=member.mention)
            )
            embed.add_field(name=t(lang, "mod_reason"), value=reason, inline=False)
            embed.add_field(name=t(lang, "mod_moderator"), value=ctx.author.mention, inline=True)
            embed.set_footer(text=t(lang, "mod_user_id").format(user_id=member.id))
            
            await ctx.send(embed=embed)
        except discord.Forbidden:
            await ctx.send(t(lang, "mod_no_permission_unmute"))
        except Exception as e:
            await ctx.send(t(lang, "mod_error_generic").format(error=e))


async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(Moderation(bot))
