"""
General commands cog.
Contains general utility and information commands.
"""

import discord
from discord.ext import commands
import platform
import time


class General(commands.Cog):
    """General utility commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """
        Check the bot's latency.
        
        Usage: !ping
        """
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: **{latency}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='info', aliases=['botinfo', 'about'])
    async def info(self, ctx):
        """
        Display information about the bot.
        
        Usage: !info
        """
        uptime = time.time() - self.start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        embed = discord.Embed(
            title="ℹ️ Bot Information",
            description="ARMA 3 Community Discord Bot",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Bot",
            value=f"{self.bot.user.name}#{self.bot.user.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Servers",
            value=f"{len(self.bot.guilds)}",
            inline=True
        )
        embed.add_field(
            name="Users",
            value=f"{sum(guild.member_count for guild in self.bot.guilds)}",
            inline=True
        )
        embed.add_field(
            name="Uptime",
            value=f"{hours}h {minutes}m {seconds}s",
            inline=True
        )
        embed.add_field(
            name="Python Version",
            value=platform.python_version(),
            inline=True
        )
        embed.add_field(
            name="Discord.py Version",
            value=discord.__version__,
            inline=True
        )
        
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='serverinfo', aliases=['server', 'guild'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """
        Display information about the current server.
        
        Usage: !serverinfo
        """
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f"ℹ️ {guild.name}",
            color=discord.Color.blue()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        embed.add_field(
            name="Owner",
            value=guild.owner.mention if guild.owner else "Unknown",
            inline=True
        )
        embed.add_field(
            name="Members",
            value=guild.member_count,
            inline=True
        )
        embed.add_field(
            name="Channels",
            value=f"Text: {len(guild.text_channels)} | Voice: {len(guild.voice_channels)}",
            inline=True
        )
        embed.add_field(
            name="Roles",
            value=len(guild.roles),
            inline=True
        )
        embed.add_field(
            name="Server ID",
            value=guild.id,
            inline=True
        )
        embed.add_field(
            name="Created At",
            value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            inline=True
        )
        
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='userinfo', aliases=['user', 'whois'])
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        """
        Display information about a user.
        
        Usage: !userinfo [@member]
        Example: !userinfo @John
        
        If no member is specified, shows info about yourself.
        """
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"ℹ️ User Information",
            color=member.color if member.color != discord.Color.default() else discord.Color.blue()
        )
        
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        
        embed.add_field(
            name="Name",
            value=f"{member.name}#{member.discriminator}",
            inline=True
        )
        embed.add_field(
            name="Nickname",
            value=member.nick if member.nick else "None",
            inline=True
        )
        embed.add_field(
            name="User ID",
            value=member.id,
            inline=True
        )
        embed.add_field(
            name="Status",
            value=str(member.status).title(),
            inline=True
        )
        embed.add_field(
            name="Joined Server",
            value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown",
            inline=True
        )
        embed.add_field(
            name="Account Created",
            value=member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            inline=True
        )
        
        roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
        if roles:
            embed.add_field(
                name=f"Roles [{len(roles)}]",
                value=", ".join(roles) if len(", ".join(roles)) <= 1024 else f"{len(roles)} roles",
                inline=False
            )
        
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='avatar', aliases=['av', 'pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        """
        Display a user's avatar.
        
        Usage: !avatar [@member]
        Example: !avatar @John
        
        If no member is specified, shows your avatar.
        """
        member = member or ctx.author
        
        embed = discord.Embed(
            title=f"{member.name}'s Avatar",
            color=discord.Color.blue()
        )
        
        if member.avatar:
            embed.set_image(url=member.avatar.url)
            embed.add_field(
                name="Download Links",
                value=f"[PNG]({member.avatar.replace(format='png').url}) | "
                      f"[JPG]({member.avatar.replace(format='jpg').url}) | "
                      f"[WEBP]({member.avatar.replace(format='webp').url})",
                inline=False
            )
        else:
            embed.description = "This user has no custom avatar."
        
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await ctx.send(embed=embed)

    @commands.command(name="say")
    @commands.has_permissions(administrator=True)
    async def say(
        self,
        ctx: commands.Context,
        channel: discord.TextChannel | None = None,
        *,
        text: str,
        ):
        """
        Заставить бота что-то сказать в нужном канале.

        Варианты:
        !say Текст тут
            → бот пишет в текущий канал

        !say #channel Текст тут
            → бот пишет в указанный канал

        !say #channel Заголовок | Текст тут --embed
            → бот отправляет embed с title + description
        """
        use_embed = False
        flag = "--embed"

        # флаг только в конце
        if text.endswith(flag):
            use_embed = True
            text = text[:-len(flag)].strip()

        target_channel = channel or ctx.channel

        if not text:
            await ctx.send("Nothing to send.")
            return

        if use_embed:
            # парсим "Title | Body"
            title = None
            description = text

            if "|" in text:
                raw_title, raw_body = text.split("|", 1)
                title = raw_title.strip() or None
                description = raw_body.strip() or None

            embed = discord.Embed(
                 title=title,
                description=description,
                color=discord.Color.blurple(),
            )
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.display_avatar.url
                if ctx.author.display_avatar
                else None,
            )
            await target_channel.send(embed=embed)
        else:
             await target_channel.send(text)

        # чистим команду, если можем
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass



async def setup(bot):
    """Setup function to add the cog to the bot."""
    await bot.add_cog(General(bot))
